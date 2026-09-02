/// Diagram of all the systems parts
/// Shows how they connect and what they are required to do
package Model {
    requirement buttonDetection {
        doc /* The system shall detect a button state transition and generate a single event for each valid button press. */
    }

    requirement serialTransmit {
        doc /* The system shall transmit event info for monitoring*/
    }

    part myButtonTask {
        satisfy buttonDetection by myButtonTask;
        satisfy serialTransmit by myButtonTask;
    }

    part mySerialListener;
    part myDatabase;
    part myCLI;

    connection microcontrollerToHostSerial connect myButtonTask to mySerialListener;
    connect mySerialListener to myDatabase;
    connect myDatabase to myCLI;
}
