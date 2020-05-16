import gintro/gst
import strutils
import strformat

const PORT=5001

proc main =
  var pipeline: gst.Element
  var bus: gst.Bus
  var msg: gst.Message

  echo "Initializing GStreamer"
  gst.init()

  let launch = [fmt"udpsrc port={PORT}",
                "application/x-rtp,encoding-name=JPEG,payload=26",
                "rtpjpegdepay",
                "jpegdec",
                "autovideosink"]

  echo "Creating pipeline"
  pipeline = gst.parseLaunch(launch.join(" ! "))

  echo "Playing Pipeline"
  discard gst.setState(pipeline, gst.State.playing)

  bus = gst.getBus(pipeline)
  msg = gst.timedPopFiltered(bus, gst.Clock_Time_None, {gst.MessageFlag.error, gst.MessageFlag.eos})
  discard gst.setState(pipeline, gst.State.null) # is this necessary?

main()
