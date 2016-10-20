import QtQuick 1.0
import QtQuick.Controls 1.0
import QtQuick.Window 2.2
 
ApplicationWindow {
    title: qsTr("Hello World")
    width: 640
    height: 480
    visible: true
 
    BusyIndicator {
       id: busyIndication
       anchors.centerIn: parent
       // 'running' defaults to 'true'
    }
 
    Button {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        text: busyIndication.running ? "Stop Busy Indicator" : "Start Busy Indicator"
        checkable: true
        checked: busyIndication.running
        onClicked: busyIndication.running = !busyIndication.running
    }
}
