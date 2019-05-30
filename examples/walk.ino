#include <Multiservo.h>
#include "Wire.h"
Multiservo m[3][4];;
int pos = 0;  
byte speed = 50, height = 10;

void setup(void)
{
  Wire.begin();
  attach_all();
  delay(50);
   m[0][0].write(110, 250);
  m[0][1].write(110, 250);
  m[0][2].write(50, 250);
  m[0][3].write(50, 250);
  for(int i = 0; i < 4; i++)
  {
    m[1][i].write(40, 250);
    m[2][i].write(40, 250);
  }
  wait_s();
}
void attach_all()
{
  m[0][0].attach(2, 650, 2000);
  m[0][1].attach(11, 750, 2100);
  m[0][2].attach(8, 900, 2200);
  m[0][3].attach(17, 900, 2250);
  
  m[1][0].attach(1, 730, 2200);
  m[1][1].attach(10, 680, 2100);
  m[1][2].attach(7, 640, 2150);
  m[1][3].attach(16, 610, 2130);
  
  m[2][0].attach(0, 750, 2250);
  m[2][1].attach(9, 700, 2100);
  m[2][2].attach(6, 700, 2180);
  m[2][3].attach(15, 680, 2100);
  delay(50);
}
void loop()
{
    forward();
}
void wait_s()
{
  for(int i = 0; i < 3; i ++)
  {
    for(int j = 0; j < 4; j++)
    {
      while(m[i][j].isMoving())
        delay(1);
    }
  }
}
void forward()
{
  static byte move = 0;
  byte speed_1 = speed;
  byte speed_2 = 255;
  byte height_1 = constrain(height, 0, 155) + 25;
  byte height_2 = constrain(height, 25, 180) - 25;;
  switch(move)
  {
    case 0:
      m[1][0].write(height_2, speed_2);
      m[2][0].write(height_2, speed_2);
      m[1][3].write(height_2, speed_2);
      m[2][3].write(height_2, speed_2);
      wait_s();
      break;
    case 1:
      m[0][0].write(60, speed_2);
      m[0][3].write(0, speed_2);
      wait_s();
      break;
    case 2:
      m[1][0].write(height_1, speed_2);
      m[2][0].write(height_1, speed_2);
      m[1][3].write(height_1, speed_2);
      m[2][3].write(height_1, speed_2);
      wait_s();
      break;
    case 3:
      m[0][0].write(110, speed_1);
      m[0][1].write(160, speed_1);
      m[0][2].write(100, speed_1);
      m[0][3].write(50, speed_1);
      wait_s();
      break;
    case 4:
      m[1][1].write(height_2, speed_2);
      m[2][1].write(height_2, speed_2);
      m[1][2].write(height_2, speed_2);
      m[2][2].write(height_2, speed_2);
      wait_s();
      break;
    case 5:
      m[0][1].write(60, speed_2);
      m[0][2].write(0, speed_2);
      wait_s();
      break;
    case 6:
      m[1][1].write(height_1, speed_2);
      m[2][1].write(height_1, speed_2);
      m[1][2].write(height_1, speed_2);
      m[2][2].write(height_1, speed_2);
      wait_s();
      break;
    case 7:
      m[0][0].write(160, speed_1);
      m[0][1].write(110, speed_1);
      m[0][2].write(50, speed_1);
      m[0][3].write(100, speed_1);
      wait_s();
      break;
    default:
      move = 0;
      return;
      break;
  }
  move ++;
}
