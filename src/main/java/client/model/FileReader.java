package client.model;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Map;
import java.util.Optional;

import org.yaml.snakeyaml.Yaml;

public class FileReader {

    private final static  Yaml yamlServerConfigFile = new Yaml();

    private FileReader() { }

    public static Optional<String> getFromFile(String key) {

        try (InputStream is = new FileInputStream("src/main/resources/serverConfig.yaml")) {

            Map<String, String> data = yamlServerConfigFile.load(is);

            final String result = data.getOrDefault(key, null);

            if (result == null) {
                throw new IllegalArgumentException("param not exists in yaml file");
            }            

            return Optional.of(result);

        } catch (Exception e) {
            e.printStackTrace();
        }   

        return Optional.empty();
    }

}
