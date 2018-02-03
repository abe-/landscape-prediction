float x, y;
float vx, vy;
float dim;
color c;
String folder;
int numframes = 33;
int NUM_TRAIN = 200;
int NUM_VAL = 60;
int NUM_TEST = 18;
int count;
boolean export = false;

void setup() {
  size(64, 64);
    reset();
}

void reset() {
  String base = "";
  if (count < NUM_TRAIN) base = "Train-gen0/";
  else if (count < NUM_TRAIN+NUM_VAL) base = "Val-gen0/";
  else if (count < NUM_TRAIN+NUM_VAL+NUM_TEST) base = "Test-gen0/";

  folder = base + nf(count, 4);
  count = count + 1;
  
  c = color(random(255), random(255), random(255));
  x = random(10, width-10);
  y = random(10, width-10);
  dim = random(6, 30);
  vx = random(-1, 1);
  vy = random(-1, 1);
}

void draw() {
  background(0);
  
  stroke(200);
  for (int xn = 0; xn < width+1; xn += 8) line(xn, 0, xn, height);
  for (int yn = 0; yn < height+1; yn += 8) line(0, yn, width, yn);
  int fc = frameCount%numframes; 
  if (fc==0) reset();

  noStroke();
  fill(c);
  ellipse(x, y, dim, dim);
  x += vx;
  y += vy;
  if (export) {
    save(folder+"/"+nf(fc-1, 3)+".png");
  }
  if (count >= NUM_TRAIN + NUM_VAL + NUM_TEST) exit();
}