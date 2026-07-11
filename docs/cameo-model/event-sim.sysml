package Model {
    part def ButtonTask;
    part def EventQueue;
    part def AlertTask;
    part def SerialListener;
    part def Database;
    part def CLI;
    requirement def ButtonDetectionReq {
        doc /* The system shall detect a button state transition and generate a single event for each valid button press. */
    }
    requirement def SerialTransmitReq {
        doc /* The alert task shall retrieve queued events and transmit event information through the serial interface for external monitoring. */
    }
    requirement def EventQueueTransferReq {
        doc /* The system shall transfer generated events between independent tasks using an event queue mechanism. */
    }
    requirement buttonDetection : ButtonDetectionReq;
    requirement serialTransmit : SerialTransmitReq;
    requirement eventQueueTransfer : EventQueueTransferReq;
    part myButtonTask : ButtonTask {
        satisfy buttonDetection;
    }
    part myEventQueue : EventQueue {
        satisfy eventQueueTransfer;
    }
    part myAlertTask : AlertTask {
        satisfy serialTransmit;
    }
    part mySerialListener : SerialListener;
    part myDatabase : Database;
    part myCLI : CLI;
    connection connect myButtonTask to myEventQueue;
    connection connect myEventQueue to myAlertTask;
    connection microcontrollerToHostSerial connect myAlertTask to mySerialListener;
    connection connect mySerialListener to myDatabase;
    connection connect myDatabase to myCLI;
}
