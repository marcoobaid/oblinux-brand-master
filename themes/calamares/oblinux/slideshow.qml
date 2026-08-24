import QtQuick 2.15
Rectangle {
  width: 800; height: 450; color: "#F4F6F8"
  property int currentSlide: 0
  property var slides: ["01-welcome.svg", "02-freedom.svg", "03-open.svg", "04-secure.svg", "05-creative.svg", "06-built.svg", "07-ready.svg"]
  Image { source: "slideshow/" + slides[parent.currentSlide]; anchors.fill: parent; fillMode: Image.PreserveAspectFit }
  Timer { interval: 7000; running: true; repeat: true; onTriggered: parent.currentSlide = (parent.currentSlide + 1) % parent.slides.length }
}
