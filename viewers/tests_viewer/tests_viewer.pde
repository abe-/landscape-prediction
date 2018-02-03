import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

PImage[][] orig;
PImage[][] pred;
ArrayList <File> folders;
int fr, fr0;

boolean gif = false;
boolean auto = true;  
String basedir = "";
float w = 200;
boolean selected = false;

int NT = 15;
int extrap = 10;
int NUMBER_OF_COLUMNS = 6;

void setup() {
  size(1200, 600);
  textAlign(LEFT, CENTER);
  textFont(createFont("Arial", 24, true));
  textSize(24);

  folders = new ArrayList();
  selectFolder("Select a folder with tests", "folderSelected");
}

void folderSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
    exit();
  } else {
    println("User selected " + selection.getAbsolutePath());
    basedir = selection.getAbsolutePath();
    buildFolderList();
    pred = new PImage[folders.size()][NT];

    for (int j = 0; j < folders.size(); j++) {
      for (int t = 0; t < NT; t++) { 
        String name = folders.get(j).getName();
        String path = new File(basedir, name).toString();
        String img = new File(path, "pred-"+nf(t, 2) + ".png").toString();
        if (t < extrap) 
        img = new File(path, "orig-"+nf(t, 2) + ".png").toString(); 
       
        pred[j][t] = loadImage(img);
        println("hola" + img);
      }
    }
    selected = true;
    fr0 = frameCount;
  }
}

void draw() {
  background(fr > (extrap)-1 ? 100 : 0);
  if (selected) {
    for (int j = 0; j < folders.size(); j++) {
      float x = j%NUMBER_OF_COLUMNS*w;
      float y = j/NUMBER_OF_COLUMNS*w;
      image(pred[j][fr], x, y, w, w);
    }

    // PREDICTED label
    if (fr > extrap-1) {
      noStroke();
      fill(0, 255, 255, 100);
      rectMode(CENTER);
      rect(width/2, 30, 200, 35);
      rectMode(CORNER);
      fill(255);
      textSize(24);
      text("PREDICTED", width/2, 38);
    }

    translate(0, height-100);

    // time axis
    strokeWeight(5);
    stroke(255);
    float paso = (width-30.-60)/(NT-1);
    float xextra = 0;
    for (int n = 0; n < NT; n++) {
      float x = 60+15+paso*n;
      line(x, 55, x, 65);
      if (n == extrap) xextra = x;
    }

    // prediction line
    noStroke();
    fill(100, 255, 255, 100);
    rect(xextra-5, 40, width-5-xextra, 40);

    fill(255, 200);
    noStroke();
    // year indicator
    rect(60+15+paso*fr-5, 45, 10, 30);
    // year text
    fill(255);
    rect(10, 42, 59, 34);
    fill(50);
    textSize(20);
    textAlign(CENTER);
    text(1984+fr, 38, 65);

    if (gif) {
      auto = false;
      saveFrame("g###.png");
      fr = frameCount-fr0;
      if (fr > NT-1) {
        noLoop();
        exit();
      }
    }


    if (auto) {
      if (frameCount%5==0)fr = fr + 1;
    }

    if (auto) fr = fr%NT;

    else if (!gif) fr = floor(map (mouseX, 0, width, 0, NT));
  }
}

void keyReleased() {
  if (selected) {
    if (key == 'a') auto = !auto;
    if (keyCode == LEFT) fr = (fr - 1) % NT;
    if (fr < 0) fr = NT - 1;
  }
}

void buildFolderList() {
  println("[DEBUG] basedir: " + basedir);
  File file = new File(basedir); 
  if (file.isDirectory()) {
    File[] files = file.listFiles();
    for (int n = 0; n < files.length; n++) {
      if (files[n].isDirectory()) {
        String path = files[n].getAbsolutePath();
        folders.add(files[n]);
      }
    }
  }
}