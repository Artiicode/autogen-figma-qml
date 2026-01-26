import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    width: 400
    height: 300
    visible: true
    title: "SystemMonitor"

    Rectangle {
        x: 20
        y: 30
        width: 360
        height: 80
        radius: 12
        color: "#2a2a4a"
    }

    Text {
        x: 60
        y: 45
        text: "CPU Usage"
        font.pixelSize: 16
        color: "#ffffff"
    }

    Text {
        x: 60
        y: 65
        text: "75%"
        font.pixelSize: 24
        color: "#00ffcc"
    }

    Rectangle {
        x: 20
        y: 130
        width: 360
        height: 80
        radius: 12
        color: "#333355"
    }

    Text {
        x: 60
        y: 145
        text: "RAM Usage"
        font.pixelSize: 16
        color: "#ffffff"
    }

    Text {
        x: 60
        y: 165
        text: "65%"
        font.pixelSize: 24
        color: "#00ccff"
    }

    Rectangle {
        x: 10
        y: 45
        width: 12
        height: 12
        radius: 6
        color: "#00ffcc"
    }

    Rectangle {
        x: 10
        y: 155
        width: 12
        height: 12
        radius: 6
        color: "#00ccff"
    }

}