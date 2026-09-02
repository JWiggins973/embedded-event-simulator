/// Diagram of all the systems parts
/// Shows how they connect and what they are required to do
package Model {
    requirement buttonDetection {
        doc /* The system shall detect a button state transition and generate a single event for each valid button press. */
    }

    requirement serialTransmit {
        doc /* The alert task shall retrieve queued events and transmit event information through the serial interface for external monitoring. */
    }

    requirement eventQueueTransfer {
        doc /* The system shall transfer generated events between independent tasks using an event queue mechanism. */
    }

    part myButtonTask {
        satisfy buttonDetection by myButtonTask;
    }
    part myEventQueue {
        satisfy eventQueueTransfer by myEventQueue;
    }
    part myAlertTask {
        satisfy serialTransmit by myAlertTask;
    }
    part mySerialListener;
    part myDatabase;
    part myCLI;

    connect myButtonTask to myEventQueue;
    connect myEventQueue to myAlertTask;
    connection microcontrollerToHostSerial connect myAlertTask to mySerialListener;
    connect mySerialListener to myDatabase;
    connect myDatabase to myCLI;
}
