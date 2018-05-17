float x, y;
float vx, vy;
float dim;
color c;
String folder;
int numframes = 32;
int count;
PImage form;

void setup() {
  size(64, 64);
  reset();
  form = loadImage("form.png");
}

void reset() {
  count = floor(frameCount/numframes);
  String base = "";
  if (count < 200) base = "Train-gen0/";
  else if (count < 250) base = "Val-gen0/";
  else if (count < 260) base = "Test-gen0/";
 
  folder = base + nf(count, 4);
  c = color(random(255), random(255), random(255));
  x = random(10, width-10);
  y = random(10, width-10);
  dim = 3*random(6, 30);
  vx = random(-1, 1);
  vy = random(-1, 1);
  folder = "Test-gen0-png/"+ nf(count, 4);
}
void draw() {
  background(0);
  stroke(200);
  for (int xn = 0; xn < width+1; xn += 8) line(xn, 0, xn, height);
  for (int yn = 0; yn < height+1; yn += 8) line(0,yn,width,yn);
  int fc = frameCount%numframes; 
  if (fc==0) reset();
  if (count < 10) {
    noStroke();
    fill(c);
    image(form,x, y, dim, dim);
    x += vx;
    y += vy;
    save(folder+"/"+nf(fc-1, 3)+".png");
  }
}