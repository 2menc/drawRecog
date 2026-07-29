package client.model.connection;

import java.awt.image.BufferedImage;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

import javax.imageio.ImageIO;

import client.model.FileReader;

public class Sender {

    private final int serverPort;
    private final String serverAddress;

    public Sender() {
        if (FileReader.getFromFile("serverAddress").isPresent()) {
            serverAddress = FileReader.getFromFile("serverAddress").get();
        } else {
            throw new IllegalArgumentException("param not exists in yaml file");
        }
        if (FileReader.getFromFile("serverPort").isPresent()) {
            serverPort = Integer.parseInt(FileReader.getFromFile("serverPort").get());
        } else {
            throw new IllegalArgumentException("param not exists in yaml file");
            }
    }

    public void sendFile(BufferedImage imageToSend) {
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
                        
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }

    }
}
