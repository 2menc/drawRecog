package client.view;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Toolkit;

import javax.swing.JFrame;

public class MainFrame extends JFrame{

    private final Toolbar toolbar;
    private final DrawPanel canvas;

    public MainFrame() {
        this.setLayout(new BorderLayout());

        final Dimension screenDimension = Toolkit.getDefaultToolkit().getScreenSize();
        final Dimension targetDimension = new Dimension(screenDimension.width/3, screenDimension.height/3);

        this.toolbar = new Toolbar();
        this.canvas = new DrawPanel();

        this.add(this.toolbar, BorderLayout.PAGE_START);
        this.add(this.canvas, BorderLayout.CENTER);

        this.setSize(targetDimension);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
        this.setVisible(true);
    }

    public DrawPanel getDrawPanel() {
        return this.canvas;
    }

    public Toolbar getToolbar() {
        return this.toolbar;
    }

}
