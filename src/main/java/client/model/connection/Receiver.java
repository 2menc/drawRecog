package client.model.connection;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;

public class Receiver {

    String receivedResult;

    public Receiver() {}

    public String receive(InputStream is) {

        try {
            DataInputStream dataIn = new DataInputStream(is);

            int responseLength = dataIn.readInt();
            byte[] responseByte = new byte[responseLength];
            dataIn.readFully(responseByte);

            receivedResult = new String(responseByte, "UTF-8");
            return receivedResult;
        
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }

    }

    public String getReceivedResult() {
        return this.receivedResult;
    }

}
