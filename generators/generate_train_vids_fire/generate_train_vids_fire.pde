// https://en.wikipedia.org/wiki/Forest-fire_model

int state[][], nextstate[][]; // 0-fire; 1-tree; 2-void
float p = 0.005;
float f = 0.00001;
int nx, ny;
color c0, c1, c2;

// GEN TRAIN
String folder;
int numframes = 33;
int NUM_TRAIN = 1000/4;
int NUM_VAL = 200/4;
int NUM_TEST = 18;
int count;
boolean export = true;

void setup() {
  size(128, 128);
  nx = width/2;
  ny = height/2;
  init();
}

void init() {
  state = new int[nx][ny];
  nextstate = new int[nx][ny];
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      state[i][j] = (random(1) > 0.6) ? 1:2;
      nextstate[i][j] = state[i][j];
    }
  }
  
  int num = floor(random(1,3));
  for (int n = 0; n < num; n++) {
    int i = floor(random(nx));
    int j = floor(random(ny));
    state[i][j] = 0;
  }  
  
  //c0 = color(random(255),random(255),random(255));
  //c1 = color(random(255),random(255),random(255));
  //c2 = color(255-red(c1),255-green(c1),255-blue(c1));
  c0 = color(255);
  c1 = color(250,200,50);
  c2 = color(0, 150, 50);
}

// GEN TRAIN
void reset() {
  String base = "";
  if (count < NUM_TRAIN) base = "Train/";
  else if (count < NUM_TRAIN+NUM_VAL) base = "Val/";
  else if (count < NUM_TRAIN+NUM_VAL+NUM_TEST) base = "Test/";

  init();

  folder = base + nf(count, 4);
  count = count + 1;
}


void draw() {
  // GEN TRAIN
  int fc = frameCount%numframes; 
  if (fc==0) reset();
  
  // Simulation
  background(0);
  strokeWeight(2);
  
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      if (state[i][j] == 2) stroke(c2);
      else if (state[i][j] == 1) stroke(c1);
      else stroke(c0);
      point(i*2, j*2);
    }
  }
  
  next();
  
  // GEN TRAIN
  if (export) {
    save(folder+"/"+nf(fc, 3)+".jpg");
  }
  if (count >= NUM_TRAIN + NUM_VAL + NUM_TEST) exit();  
}

// Simulation
void next() {
  // a burning tree becomes an empty space
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      if (state[i][j] == 0) nextstate[i][j] = 2;
    }
  }
  
  // new tree  
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      if (state[i][j] == 2) {
        if (random(1) < p) nextstate[i][j] = 1;
      }
    }
  }
  
  // new fire
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      if (state[i][j] == 1) {
        if (random(1) < f) nextstate[i][j] = 0;
      }
    }
  }
  
  // burns if a neighbour is in fire
  for (int i = 1; i < nx-1; i++) {
    for (int j = 1; j < ny-1; j++) {
      if (state[i][j] == 1) {
        if (state[i-1][j]*state[i+1][j]*state[i][j-1]*state[i][j+1]*state[i-1][j-1]*state[i-1][j+1]*state[i+1][j-1]*state[i+1][j+1] == 0) {
          nextstate[i][j] = 0;
        }
      }
    }
  }
  
  // update state
  for (int i = 0; i < nx; i++) {
    for (int j = 0; j < ny; j++) {
      state[i][j] = nextstate[i][j];
    }
  }
}