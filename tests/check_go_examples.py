#!/usr/bin/env python3
"""Compile the repository's exact non-normative Go fragments offline."""
from pathlib import Path
import argparse, os, re, shutil, subprocess, tempfile

if shutil.which("go") is None:
    raise SystemExit("A local Go toolchain is required for this optional example check.")

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
a = p.parse_args()
def blocks(path):
    return re.findall(r'^```go\n(.*?)^```$',(a.root/path).read_text(),re.M|re.S)
with tempfile.TemporaryDirectory(prefix='spec-go-examples-') as tmp:
    root=Path(tmp)
    def write(name,content):
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    write('go.mod','module example.test/spec-examples\n\ngo 1.20\n')
    go=blocks('specification/languages/go.md');assert len(go)==1
    write('basic/example.go','package basic\nimport("errors";"net/url")\n'+go[0])
    write('basic/example_test.go','''package basic
import "testing"
func TestParser(t *testing.T) {
 if _,err:=ParseCreateCommand(CreateRequest{}); err==nil { t.Fatal("missing name accepted") }
 got,err:=ParseCreateCommand(CreateRequest{Name:"valid"}); if err!=nil || got.name!="valid" { t.Fatal(got,err) }
}
''')
    options=blocks('specification/languages/go/functional-options.md');assert len(options)==3
    write('options/example.go','package options\nimport("errors";"fmt";"time")\n'+options[0]+options[2])
    write('options/example_test.go','''package options
import("testing";"time";"errors")
func TestCallSite(t *testing.T) {
'''+options[1]+'''
 if err!=nil || server==nil { t.Fatal(err) }
}
func TestDefaultAndOrder(t *testing.T) {
 base,err:=NewServer("local");if err!=nil || base.options.timeout!=30*time.Second { t.Fatal(base,err) }
 changed,err:=NewServer("local",WithTimeout(time.Second),WithTimeout(2*time.Second));if err!=nil || changed.options.timeout!=2*time.Second { t.Fatal(changed,err) }
}
func TestInvalidOptions(t *testing.T) {
 for _,options:=range [][]ServerOption{{nil},{WithTimeout(0)}} {
  got,err:=NewServer("local",options...);if got!=nil || !errors.Is(err,ErrInvalidServerOption) { t.Fatal(got,err) }
 }
}
func TestWorkerConfig(t *testing.T) {
 if _,err:=NewWorker(WorkerConfig{});err==nil {t.Fatal("invalid config accepted")}
 if _,err:=NewWorker(WorkerConfig{Queue:"jobs",Workers:2});err!=nil {t.Fatal(err)}
}
''')
    factory=blocks('specification/languages/go/factory-delegation.md');assert len(factory)==3
    write('factory/example.go','package factory\nimport("context";"errors";"fmt")\n'+factory[0]+factory[1])
    write('factory/example_test.go','''package factory
import("testing";"context";"errors")
type handler struct{}
func (*handler) HandleMessage(context.Context,string) error {return nil}
func TestAbsentAndNilDelegate(t *testing.T) {
 f,err:=NewFactory("plugin");if err!=nil || f.Supports(CapabilityMessages) {t.Fatal(f,err)}
 got,err:=f.CreateMessageHandler(context.Background(),MessageConfig{Route:"r"})
 if got!=nil || !errors.Is(err,ErrCapabilityNotSupported) {t.Fatal(got,err)}
 var fn CreateMessageHandlerFunc
 if f,err:=NewFactory("p",WithMessageHandler(fn));f!=nil || !errors.Is(err,ErrInvalidFactoryOption) {t.Fatal(f,err)}
}
func TestDispatchIdentity(t *testing.T) {
 ctx:=context.Background(); calls:=0; want:=&handler{}
 f,err:=NewFactory("p",WithMessageHandler(func(c context.Context,config MessageConfig)(MessageHandler,error) {
  calls++;if c!=ctx || config.Route!="r" {t.Fatal("arguments changed")};return want,nil
 }))
 if err!=nil {t.Fatal(err)}
 got,err:=f.CreateMessageHandler(ctx,MessageConfig{Route:"r"});if err!=nil || got!=want || calls!=1 {t.Fatal(got,err,calls)}
}
func TestDelegateError(t *testing.T) {
 want:=errors.New("delegate failed")
 f,err:=NewFactory("p",WithMessageHandler(func(context.Context,MessageConfig)(MessageHandler,error){return nil,want}))
 if err!=nil {t.Fatal(err)}
 _,err=f.CreateMessageHandler(context.Background(),MessageConfig{Route:"r"});if !errors.Is(err,want) || errors.Is(err,ErrCapabilityNotSupported) {t.Fatal(err)}
}
func TestNilResultCannotBeSuccess(t *testing.T) {
 f,err:=NewFactory("p",WithMessageHandler(func(context.Context,MessageConfig)(MessageHandler,error){return nil,nil}))
 if err!=nil {t.Fatal(err)}
 got,err:=f.CreateMessageHandler(context.Background(),MessageConfig{Route:"r"})
 if got!=nil || err==nil {t.Fatal("example returned successful nil handler",got,err)}
}
''')
    shared=factory[0].split('type MessageConfig',1)[1].split('type factoryOptions',1)[0]
    write('closed/example.go','package closed\nimport "context"\ntype MessageConfig'+shared+factory[2])
    env=dict(os.environ,GOTOOLCHAIN='local',GOPROXY='off',GOSUMDB='off',GOWORK='off')
    print(subprocess.check_output(['go','version'],text=True).strip(),flush=True)
    raise SystemExit(subprocess.run(['go','test','-count=1','-v','./...'],cwd=root,env=env,timeout=90).returncode)
