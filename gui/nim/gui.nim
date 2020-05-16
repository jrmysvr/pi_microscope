import webgui, osproc
echo currentHtmlPath()
let app = newWebView(currentHtmlPath())

var pid: owned(Process)

app.bindProcs("api"):
  # proc callback() = echo execCmd("./nim_consumer")
  proc startCallback() =
    pid = startProcess("./nim_consumer")

  proc stopCallback() =
    if not (pid == nil) :
      echo "Stopping Stream ", $pid.processID()
      terminate(pid)

app.run()
app.exit()
