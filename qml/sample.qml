import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    width: 900
    height: 600
    visible: true
    title: "Auto GUI"

    Rectangle {
        id: hero
        x: 40
        y: 40
        width: 820
        height: 240
        radius: 24
        color: "#F2F2F2"

        Text {
            x: 20
            y: 20
            text: "Auto GUI"
            font.pixelSize: 32
            color: "#111111"
        }
    }

    Rectangle {
        id: cta
        x: 40
        y: 320
        width: 820
        height: 80
        radius: 12
        color: "#111111"

        Text {
            anchors.centerIn: parent
            text: "Get Started"
            font.pixelSize: 20
            color: "#FFFFFF"
        }
    }
}
