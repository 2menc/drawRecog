package client.model.connection;

import java.awt.image.BufferedImage;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

import javax.imageio.ImageIO;

import client.model.FileReader;

public class NetworkClient {

    String receivedResult;

    private final int serverPort;
    private final String serverAddress;

    public NetworkClient() {

        if (FileReader.getStringFromFile("serverAddress").isPresent()) {
            serverAddress = FileReader.getStringFromFile("serverAddress").get();
        } else {
            throw new IllegalArgumentException("param not exists in yaml file");
        }
        if (FileReader.getStringFromFile("serverPort").isPresent()) {
            serverPort = Integer.parseInt(FileReader.getStringFromFile("serverPort").get());
        } else {
            throw new IllegalArgumentException("param not exists in yaml file");
        }
    }


    public String sendAndReceiveImage(BufferedImage imageToSend) {
        try (
            Socket socket = new Socket(serverAddress, serverPort);

            BufferedOutputStream out = new BufferedOutputStream(socket.getOutputStream());
            DataOutputStream dataOut = new DataOutputStream(out);
        ) {

            final ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write(imageToSend, "png", baos);
            byte[] imageBytes = baos.toByteArray();

            dataOut.writeInt(imageBytes.length);
            dataOut.write(imageBytes);

            out.flush();

            String result = this.receive(socket.getInputStream());
            return result;

                        
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }

    public String sendAndReceiveModelChange(String newModel) {
        try (
            Socket socket = new Socket(serverAddress, serverPort);

            BufferedOutputStream out = new BufferedOutputStream(socket.getOutputStream());
            DataOutputStream dataOut = new DataOutputStream(out);
        ) {

            String command = newModel.startsWith("MODEL:") ? newModel : "MODEL:" + newModel;
            byte[] bytes = command.getBytes(java.nio.charset.StandardCharsets.UTF_8);

            dataOut.writeInt(bytes.length);
            dataOut.write(bytes);

            out.flush();

            String result = this.receive(socket.getInputStream());
            return result; // python server response

        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
    }
    private String receive(InputStream is) {

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


