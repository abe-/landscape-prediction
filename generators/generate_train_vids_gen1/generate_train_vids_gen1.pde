float x, y;
float vx, vy, vg;
float dim;
color c;
String folder;
int numframes = 32;
int count;

void setup() {
  size(64, 64);
  reset();
}

void reset() {
  count = floor(frameCount/numframes);
  String base = "";
  if (count < 200) base = "Train-gen1/";
  else if (count < 250) base = "Val-gen1/";
  else if (count < 260) base = "Test-gen1/";
 
  folder = base + nf(count, 4);
  c = color(random(255), random(255), random(255));
  x = random(10, width-10);
  y = random(10, width-10);
  dim = random(-10, 30);
  vg = random(1, 2);
  vx = random(-1, 1);
  vy = random(-1, 1);
}
void draw() {
  background(0);
  stroke(200);
  for (int xn = 0; xn < width+1; xn += 8) line(xn, 0, xn, height);
  for (int yn = 0; yn < height+1; yn += 8) line(0,yn,width,yn);
  int fc = frameCount%numframes; 
  if (fc==0) reset();
  if (count < 260) {
    noStroke();
    fill(c);
    ellipse(x, y, dim, dim);
    dim += vg;
    save(folder+"/"+nf(fc, 2)+".png");
  }
}