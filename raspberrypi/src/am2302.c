// gcc -o am2302 am2302.c -l bcm2835
#include <bcm2835.h>
#include <stdio.h>
#include <sched.h>
#include <sys/mman.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <arpa/inet.h>
#include <byteswap.h>

// Blinks on RPi Plug P1 pin 7 (which is GPIO pin 4)
#define PIN RPI_GPIO_P1_07
// Measure result type
union  _am2302_res{
  uint8_t byte[5];
  struct {
    uint16_t temp;
    uint16_t humd;
    uint8_t  par;
  } var;
};
int main(int argc, char **argv)
{
  int res=0;
  char timeStr[32];
  struct tm tM;
  time_t t;
  char msg[64];
  uint8_t bitsCount=0;
  uint8_t parity=0;
  union _am2302_res sample={{0}};
  // prevent swapping
  struct sched_param sp;
  memset(&sp, 0, sizeof(sp));
  sp.sched_priority = sched_get_priority_max(SCHED_FIFO);
  sched_setscheduler(0, SCHED_FIFO, &sp);
  mlockall(MCL_CURRENT | MCL_FUTURE);
    // If you call this, it will not actually access the GPIO
    // Use for testing
    //bcm2835_set_debug(1);
    if (!bcm2835_init())
      return 1;
    struct timeval now, pulse;
    int cycles, micros;
    int bits[40];
    uint8_t try=0;
    // set PIN pullUP
    bcm2835_gpio_set_pud(PIN, BCM2835_GPIO_PUD_UP);
    for(try=0;try<10;try++)
    {
        res=0;
        msg[0]='\0';
        bitsCount=0;
        time(&t);
        localtime_r(&t,&tM);
        strftime(timeStr,sizeof(timeStr),"%Y-%m-%d %H:%M:%S",&tM);
        bzero(&sample,sizeof(sample));
        // Set the pin to be an output
        bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_OUTP);
        // turn it off for 1ms
        bcm2835_gpio_write(PIN, LOW);
        bcm2835_delay(1);
        // Turn it on
        bcm2835_gpio_write(PIN, HIGH);
        // Set the pin to be an input and wait for 40us
        bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_INPT);
        bcm2835_delayMicroseconds(40);
        if(bcm2835_gpio_lev(PIN)==HIGH)
        {
          snprintf(msg,sizeof(msg),"sensor not responding");
          res=1;
          bcm2835_delay(2000);
          continue;
        }
        // Sensor pulls low for 80us
        while(bcm2835_gpio_lev(PIN)==LOW);
        // Sensor pulls high for 80us
        while(bcm2835_gpio_lev(PIN)==HIGH);
        // Began data transmission from sensor
        gettimeofday(&pulse, NULL);
        for(bitsCount=0;bitsCount<40;bitsCount++)
        {
          // Sensor pulls low for 50us
          for(cycles=0;(bcm2835_gpio_lev(PIN)==LOW)&&(cycles<1000);cycles++);
          if(cycles==1000)
          {
            snprintf(msg,sizeof(msg),"read failed on signal LOW");
            res=2;
            break;
          }
          // Sensor pulls high for 30us or 70us
          for(cycles=0;(bcm2835_gpio_lev(PIN)==HIGH)&&(cycles<1000);cycles++);
          gettimeofday(&now, NULL);
          if(cycles==1000)
          {
            snprintf(msg,sizeof(msg),"read failed on signal HIGH, count=%d",bitsCount);
            res=3;
            break;
          }
          if (now.tv_sec > pulse.tv_sec)
            micros = 1000000L;
          else
            micros = 0;
          micros = micros + (now.tv_usec - pulse.tv_usec);
          bits[bitsCount] = micros;
          pulse = now;
        }
        if(!res)
        {
          for(bitsCount=0;bitsCount<40;bitsCount++)
          {
            if(bits[bitsCount]<120)
            {
              bits[bitsCount]=0;
            }
            else
            {
              bits[bitsCount]=1;
              sample.byte[bitsCount/8] = sample.byte[bitsCount/8] | (1<<(7 - (bitsCount%8)));
            }
            //printf("%d ",bits[bitsCount]);
          }
          parity = sample.byte[0]+sample.byte[1]+sample.byte[2]+sample.byte[3];
          if(parity==sample.var.par)
          {
            sample.var.temp = __bswap_16(sample.var.temp);
            sample.var.humd = __bswap_16(sample.var.humd);
          }
          else
          {
            snprintf(msg,sizeof(msg),"parity fail");
            res=4;
          }
        }
        bcm2835_delay(2000);
        if(!res)
          break;
        //printf("\n%x %x %u=%u\n",sample.var.temp,sample.var.humd,parity,sample.byte[4]);
        //printf("%x %x %u=%u\n",sample.var.temp,sample.var.humd,parity,sample.byte[4]);
        //printf("%u %u %u=%u\n",sample.var.temp,sample.var.humd,parity,sample.byte[4]);
        //printf("%f %f %u=%u\n",sample.var.temp/10.0,sample.var.humd/10.0,parity,sample.byte[4]);
        // wait a bit
    }
    bcm2835_close();
    printf("sampletime=\"%s\"\nstatus=%d\nmessage=\"%s\"\ntemperature=%u\nhumidity=%u\n",timeStr,res,msg,sample.var.humd,sample.var.temp);
    return res;
}
