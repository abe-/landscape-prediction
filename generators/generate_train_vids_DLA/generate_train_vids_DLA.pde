
// GEN TRAIN
String folder;
int numframes = 33;
int NUM_TRAIN = 1000;
int NUM_VAL = 100;
int NUM_TEST = 18;
int count;
boolean export = true;

// https://www.openprocessing.org/sketch/125643
//Based on program from Generative Design book by Hartmut Bohnacker
//Processing 2.0

int max = 25000;                //maximum number of particles
int countDLA = 1;
float[] x;
float[] y;
float r = 1;                    //line length
PVector axis;
float dec=0.9999;               //decrease rate of stroke weight

void setup() {
  size(128, 128);
  smooth();
  stroke(250);
  strokeWeight(3);
  x = new float[max];
  y = new float[max];
  init();
}


void init() {
  for (int n = 0; n < x.length; n++) {
    x[n] = -10000;
    y[n] = -10000;
  }
  x[0] = width/2;               //initial particle position
  y[0] = height/2;            //
  countDLA = 0;
  
  background(0,60,60);
}

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
  int fc = frameCount%numframes; 
  if (fc==0) reset();

  for (int n = 0; n < 5; n++) {
    
    axis = new PVector(random(10, width-10), random(10, height-10));
    float minDist = 1000;
    int pin = 0;
    for (int i=0; i < countDLA; i++) {                      //find the closest particle of the organism
      float updtDist = dist(axis.x, axis.y, x[i], y[i]);
      if (updtDist < minDist) {
        minDist = updtDist;
        pin = i;
      }
    }
    float theta = atan2(axis.y-y[pin], axis.x-x[pin]);
    x[countDLA] = x[pin] + cos(theta) * r*2;
    y[countDLA] = y[pin] + sin(theta) * r*2;
    line(x[countDLA], y[countDLA], x[pin], y[pin]);              //attach new particle to the organism
    countDLA++;
    if (dec>=0.3) {  
      dec-=0.0001;
    }                      //restrain minimum stroke weight
    else {  
      dec=0.3;
    }
  }


  if (export) {
    save(folder+"/"+nf(fc, 3)+".png");
  }
  if (count >= NUM_TRAIN + NUM_VAL + NUM_TEST) exit();
}