import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

// Interface
int nX = 4;
int nY = 2;
float border = 40;
float W = 256, H = 256;
boolean sel[][];

// Images
ArrayList <File> folders;
String basedir;
ArrayList[][] imgs;
File[][] currentFolders;

// Images in display
int count = 0;
float frame = 0;

// Trash
String trashdir;
File trash;
boolean selected = false;

void setup() {
  size(1150, 610, P2D);
  sel = new boolean[nX][nY];
  imgs = new ArrayList[nX][nY];
  currentFolders = new File[nX][nY];

  for (int i = 0; i < nX; i++) 
    for (int j = 0; j < nY; j++) 
      imgs[i][j] = new <PImage> ArrayList();

  folders = new ArrayList();
  selectFolder("Select a folder to process:", "folderSelected");
}


void folderSelected(File selection) {
  if (selection == null) {
    println("Window was closed or the user hit cancel.");
    exit();
  } else {
    println("User selected " + selection.getAbsolutePath());
    basedir = selection.getAbsolutePath();
    buildFolderList();

    String parentPath = new File(basedir).getParent();
    trash = new File(parentPath, "Trash");
    trashdir = trash.toString();
    if (!trash.exists()) trash.mkdir();

    loadImages();
    selected = true;
  }
}

void loadImages() {
  for (int i = 0; i < nX; i++) {
    for (int j = 0; j < nY; j++) {
      sel[i][j] = false;
      imgs[i][j].clear();
      int id = min(count + j*nX + i, folders.size()-1);
      File folder = folders.get(id);
      currentFolders[i][j] = folder;
      if (currentFolders[i][j].exists()) {
        File images[] = folder.listFiles();
        for (int n = 0; n < images.length; n++) {
          imgs[i][j].add( loadImage( images[n].getAbsolutePath() ));
        }
      }
    }
  }
}

void draw() {
  background(30, 30, 40);
  if (selected) {
    for (int i = 0; i < nX; i++) {
      for (int j = 0; j < nY; j++) {
        float x = map(i, 0, nX, border, width-20);
        float y = map(j, 0, nY, border, height-20);
        stroke(255, sel[i][j]?255:0);
        fill(255, 0);
        rect(x-.5, y-.5, W+1, H+1);
        if (currentFolders[i][j].exists() && imgs[i][j].get(floor(frame)) != null) {
          PImage tmp = (PImage) imgs[i][j].get(floor(frame));
          image(tmp, x, y, W, H);
        }
      }
    }
    frame = frame + .25;
    if ( frame > 32 ) frame = 0;
    if ( frame < 0 ) frame = 32;

    fill(220);
    textAlign(CENTER);
    text("- "+ floor(count/8.) + "/" + floor(folders.size()/8.)+ " -", width/2, height-15);
  }
}

void mouseReleased()  {
  if (selected) {
    for (int i = 0; i < nX; i++) {
      for (int j = 0; j < nY; j++) {
        float x = map(i, 0, nX, border, width-20);
        float y = map(j, 0, nY, border, height-20);
        if ( mouseOverRect(x, y, W, H)) sel[i][j] = !sel[i][j];
      }
    }
  }
}

void keyPressed() {
  if (selected) {
    if (keyCode == RIGHT) {
      count = constrain(count+nX*nY, 0, folders.size()-1);
      loadImages();
    }
    if (keyCode == LEFT) {
      count = constrain(count-nX*nY, 0, folders.size()-1);
      loadImages();
    }
    if (frame > 32) frame = 0;
    if (frame < 0) frame = 32;
  }
}

void keyReleased() {
  if (selected) {
    if (key == 'd' || keyCode == BACKSPACE) {
      for (int i = 0; i < nX; i++) {
        for (int j = 0; j < nY; j++) {
          if (sel[i][j]) {
            deleteFolder(currentFolders[i][j]);
          }
        }
      }
    }
  }
}

boolean mouseOverRect(float x_, float y_, float w_, float h_) {
  return mouseX>x_&&mouseX<x_+w_&&mouseY>y_&&mouseY<y_+h_;
}


void deleteFolder(File f) {  
  if (f.exists()) {
    Path dest = Paths.get(trash.getAbsolutePath(), f.getName());
    try {
      Files.move(f.toPath(), dest);
    } 
    catch (IOException e) {
      System.err.println(e);
    }
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