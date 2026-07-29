package client.view;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.ArrayList;
import java.util.List;

public class DrawPanel extends JPanel {

    private final List<Point> pixels = new ArrayList<>();

    public DrawPanel() {
        setBackground(Color.WHITE); 

        MouseAdapter gestoreMouse = new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                pixels.add(e.getPoint());
                repaint();
            }

            @Override
            public void mouseDragged(MouseEvent e) {
                pixels.add(e.getPoint()); 
                repaint(); 
            } 

            @Override
            public void mouseReleased(MouseEvent e) {
                pixels.add(null); 
                repaint();
            }
        };

        addMouseListener(gestoreMouse);
        addMouseMotionListener(gestoreMouse);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;

        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setStroke(new BasicStroke(4f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)); 
        g2.setColor(Color.BLACK);

        for (int i = 0; i < pixels.size(); i++) {
            Point p1 = pixels.get(i);
            
            if (p1 == null) {
                continue;
            }

            Point p2 = (i + 1 < pixels.size()) ? pixels.get(i + 1) : null;

            if (p2 != null) {
                // links two consecutive points
                g2.drawLine(p1.x, p1.y, p2.x, p2.y);
            } else {
                // manages click without dragging
                g2.drawLine(p1.x, p1.y, p1.x, p1.y);
            }
        }
    }

    public List<Point> getDrawing() {
        return new ArrayList<>(pixels);
    }

    public void eraseAll() {
        this.pixels.replaceAll(p -> null);
        this.paintComponent(getGraphics());
        this.revalidate();
        this.repaint();
    }
}