import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    width: 800
    height: 600
    visible: true
    title: "dashboard"

    Rectangle {
        x: 0
        y: 0
        width: 800
        height: 600
        radius: 10
        color: "#1e1e2f"
    }

    Rectangle {
        x: 20
        y: 20
        width: 300
        height: 150
        radius: 10
        color: "#2d2d44"
    }

    Text {
        x: 40
        y: 40
        text: "CPU Usage"
        font.pixelSize: 18
        color: "#ffffff"
    }

    Text {
        x: 40
        y: 70
        text: "75%"
        font.pixelSize: 36
        color: "#00ffcc"
    }

    Rectangle {
        x: 340
        y: 20
        width: 300
        height: 150
        radius: 10
        color: "#2d2d44"
    }

    Text {
        x: 360
        y: 40
        text: "RAM Usage"
        font.pixelSize: 18
        color: "#ffffff"
    }

    Text {
        x: 360
        y: 70
        text: "65%"
        font.pixelSize: 36
        color: "#00ccff"
    }

}