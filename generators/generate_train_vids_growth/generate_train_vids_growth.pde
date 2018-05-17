ArrayList <PVector> ps;

// GEN TRAIN
String folder;
int numframes = 33;
int NUM_TRAIN = 1000;
int NUM_VAL = 200;
int NUM_TEST = 18;
int count;
boolean export = true;

void setup() {
  size(128, 128);
  init();
}

// Simulation
void init() {
  ps = new ArrayList();
  ps.add( new PVector(width/2, height/2) );
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
  background(255);
  for (int n = 0; n < 255; n++) newParticle();
  fill(0, 200);
  noStroke();
  
  for (PVector p : ps) {
    PVector center = new PVector(width/2, height/2);
    PVector p2 = p.copy();
    p2.sub(center);
    float angle = p2.heading();
    float d = p2.mag();
    float amp = map(sqrt(d), 0, sqrt(width/2), 0.5, 0);
    arc(width/2, height/2, d*2, d*2, angle-amp, angle+amp);
  }
  
  // GEN TRAIN
  if (export) {
    save(folder+"/"+nf(fc, 3)+".jpg");
  }
  if (count >= NUM_TRAIN + NUM_VAL + NUM_TEST) exit();
}

// Simulation
void newParticle() {
  PVector pos = new PVector(width/2, height/2);
  pos.add(randomGaussian()*width/2, randomGaussian()*height/2);
  boolean col = false;
  for (PVector p : ps) {
    if (p.dist(pos) < 5) col = true;
  }
  if (col) ps.add(pos);
}