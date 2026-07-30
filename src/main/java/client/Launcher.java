package client;

import client.controller.Controller;
import io.github.cdimascio.dotenv.Dotenv;

public class Launcher {

    public static void main(String[] args) {

        final Dotenv dotenv = Dotenv.load();

        final String serverIp = dotenv.get("TAILSCALE_SERVER_IP");
        
        new Controller(serverIp);
        
    }

}
