#include <Wire.h>
#include <Multiservo.h>
#include <math.h>
#define sqr(x) ((x)*(x))
#define PI 3.141592653589793238
#define rad2deg(x) ((180.0/PI)*(x))
#define deg2rad(x) ((PI/180.0)*(x))
#define FemurL 4.2
#define TibiaL 7.8
int c = 40;//Femur
int a = 80;//Tibia
int t = 10;

Multiservo Coxa;
Multiservo Femur;
Multiservo Tibia;

void setup()
{
  Wire.begin();
  Coxa.attach(11, 700, 2000);
  Femur.attach(10, 620, 2350);
  Tibia.attach(9, 700, 2550);
//Tibia.write(75);
  //Femur.write(90);
  //Tibia.write(90);
/*
Coxa.attach(2, 750, 2500);
Femur.attach(1, 700, 2500);
Tibia.attach(0, 650, 2300);
*/
  Serial.begin(9600);
  move(8, -8.5);
  delay(4000);
  move(8, 8.5);
  
}
void loop()
{
  /*
   for(float i = 0; i < 8; i += 0.1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    move(i, -8);
    delay(2);                       // waits 15ms for the servo to reach the position 
  } 
  delay(500);
   for(float i = -8; i < -5; i += 0.1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    move(8, i);
    delay(2);                       // waits 15ms for the servo to reach the position 
  } 
  delay(500);
   for(float i = 8; i > 0; i -= 0.1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    move(i, -5);
    delay(2);                       // waits 15ms for the servo to reach the position 
  } 
  delay(500);
   for(float i = -5; i > -8; i -= 0.1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    move(0, i);
    delay(2);                       // waits 15ms for the servo to reach the position 
  }
  delay(500);*/
}
float polarAngle(float x, float y, float gama)
{
  if(!gama)
  {
    if(x > 0)
    {
      if(y > 0)
        return atan(x / y);
      else
        return atan(x / y) + PI;
    }
    else
    {
      if(y > 0)
        return 0;
      else
        return PI;
    }
      
  }
  else
  {
    return gama - (PI / 2 - atan(y / x));      
  }
}
void move(float x, float y)
{
  float localDestX = x, localDestY = y;
  float A = -2 * localDestX;
  float B = -2 * localDestY;
  float C = sqr(localDestX) + sqr(localDestY) + sqr(FemurL) - sqr(TibiaL);
  float X0 = -A * C / (sqr(A) + sqr(B));
  float Y0 = -B * C / (sqr(A) + sqr(B));
  float D = sqrt( sqr(FemurL) - (sqr(C) / (sqr(A) + sqr(B))) );
  float mult = sqrt ( sqr(D) / (sqr(A) + sqr(B)));
  float ax, ay, bx, by;
  ax = X0 + B * mult;
  bx = X0 - B * mult;
  ay = Y0 - A * mult;
  by = Y0 + A * mult;
  if(ax < 0)
  {
    ax = 0;
    ay = -12;
  }
  if(bx < 0)
  {
    bx = 0;
    by = -12;
  }
  // Select solution on top as joint
  float jointLocalX = (ay > by) ? ax : bx;
  float jointLocalY = (ay > by) ? ay : by;
  Serial.print("ax: ");
  Serial.print(ax);
  Serial.print("   ay: ");
  Serial.println(ay);
  Serial.print("bx: ");
  Serial.print(bx);
  Serial.print("   by: ");
  Serial.println(by);
  Serial.print("jointLocal X: ");
  Serial.print(jointLocalX);
  Serial.print("   Y: ");
  Serial.println(jointLocalY);
  float gama = polarAngle(jointLocalX, jointLocalY, false);  
  float alpha = polarAngle(localDestX - jointLocalX, localDestY - jointLocalY, gama);
  Serial.print("Alpha: ");
  Serial.print(rt(alpha / PI * 180));
  Serial.print("   Gama: ");
  Serial.println(gama / PI * 180);
  //Serial.println(localDestY - jointLocalY);
  Femur.write(int(rt(gama / PI * 180)) + 1, 40);
  Tibia.write(int(rt(alpha / PI * 180)), 40);
}
float rt(float angle)
{
  if (angle > 180)
   return angle - 180;
  else if (angle < 0)
    return angle + 180;
  else 
    return angle;
}
float Verif_asin(float asn) {
if (asn > 1) {
return 1;
}
if (asn < -1) {
return -1;
}
return asn;
}
