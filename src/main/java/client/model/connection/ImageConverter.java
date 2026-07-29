package client.model.connection;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.util.List;

public class ImageConverter {

    private ImageConverter() { }

    public static BufferedImage convertToImage(List<Point> points, Dimension windowDim) {

        final var img = new BufferedImage(windowDim.width, windowDim.height, BufferedImage.TYPE_BYTE_BINARY);

        final Graphics2D g2d = img.createGraphics();

        g2d.setColor(Color.WHITE);
        g2d.fillRect(0, 0, windowDim.width, windowDim.height);
        
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setStroke(new BasicStroke(4f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
        g2d.setColor(Color.BLACK);

        for (int i = 0; i < points.size(); i++) {
            Point p1 = points.get(i);
            if (p1 == null) {
                continue;
            }

            Point p2 = (i+1 < points.size()) ? points.get(i+1) : null;

            if (p2 != null) {
                g2d.drawLine(p1.x, p1.y, p2.x, p2.y);
            } else {
                g2d.drawLine(p1.x, p1.y, p1.x, p1.y);
            }
        }

        g2d.dispose();

        return img;        
    }
}
