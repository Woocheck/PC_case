#include "stdlib.h"
#include "pico/stdlib.h"
#include "hardware/pwm.h"

#define LED_PIN 28

struct ledRGB 
{
    int redLED;
    int greenLED;
    int blueLED;
    
};

struct colour
{
    int red;
    int blue;
    int green;
};

int returnColourIntensity( int colour, int intensity )
{
    int colourIntensity = ( 255 - colour );

    return colourIntensity;
}
void initRGB(  struct ledRGB diode )
{

    gpio_set_function(  diode.redLED, GPIO_FUNC_PWM );
    gpio_set_function(  diode.blueLED, GPIO_FUNC_PWM );
    gpio_set_function(  diode.greenLED, GPIO_FUNC_PWM );

    uint sliceRed = pwm_gpio_to_slice_num(  diode.redLED );
    uint sliceBlue = pwm_gpio_to_slice_num(  diode.blueLED );
    uint sliceGreen = pwm_gpio_to_slice_num(  diode.greenLED );

    pwm_set_wrap( sliceRed, 256 );
    pwm_set_wrap( sliceBlue, 256 );
    pwm_set_wrap( sliceGreen, 256 );

}  

void setColourRGB(  struct colour colourRGB, int intensity, struct ledRGB diode )
{    
    uint sliceRed = pwm_gpio_to_slice_num(  diode.redLED );
    uint channelRed = pwm_gpio_to_channel(  diode.redLED );
   
    uint sliceBlue = pwm_gpio_to_slice_num(  diode.blueLED );
    uint channelBlue = pwm_gpio_to_channel(  diode.blueLED );

    uint sliceGreen = pwm_gpio_to_slice_num(  diode.greenLED );
    uint channelGreen = pwm_gpio_to_channel(  diode.greenLED );

    pwm_set_chan_level( sliceRed, channelRed, returnColourIntensity( colourRGB.red, intensity ) ); 
    pwm_set_enabled( sliceRed, true ); 

    pwm_set_chan_level( sliceBlue, channelBlue, returnColourIntensity( colourRGB.blue, intensity ) ); 
    pwm_set_enabled( sliceBlue, true );

    pwm_set_chan_level( sliceGreen, channelGreen, returnColourIntensity( colourRGB.green, intensity ) ); 
    pwm_set_enabled( sliceGreen, true );
}


struct colour colorDistance( struct colour begin, struct colour final )
{
    struct colour distance = { 0, 0, 0 };

    distance.red = abs( begin.red - final.red );
    distance.blue = abs( begin.blue - final.blue );
    distance.green = abs( begin.green - final.green );

    return distance;
}

struct colour calculateIncrement( struct colour distance, int fps, int duration )
{
    struct colour increment = { 0, 0, 0 };

    increment.red = abs( distance.red / fps );
    increment.blue = abs( distance.blue / fps );
    increment.green = abs( distance.green / fps );

    return increment;
}

void transitionStep( struct colour currentColor, struct colour targetColor, struct colour increment, struct ledRGB diode )
{
    
    if( currentColor.red > targetColor.red )
    {
        currentColor.red -= increment.red;
        if( currentColor.red <= targetColor.red) 
            increment.red = 0;
    }
    else
    {
        currentColor.red += increment.red;
        if( currentColor.red >= targetColor.red )
            increment.red = 0;
    }
        
    if( currentColor.blue > targetColor.blue )
    {
        currentColor.blue -= increment.blue;
        if( currentColor.blue <= targetColor.blue) 
            increment.blue = 0;
    }
    else
    {
        currentColor.blue += increment.blue;
        if( currentColor.blue >= targetColor.blue )
            increment.blue = 0;
    }

    if( currentColor.green > targetColor.green )
    {
        currentColor.green -= increment.green;
        if( currentColor.green <= targetColor.green) 
            increment.green = 0;
    }
    else
    {
        currentColor.green += increment.green;
        if( currentColor.green >= targetColor.green )
            increment.green = 0;
    }
        

    setColourRGB( currentColor, 100, diode );
}

void colourTransition( struct colour begin, struct colour final, int fps, int durationMs, struct ledRGB diode )
{
    struct colour distance = colorDistance( begin, final);
    struct colour increment = calculateIncrement(distance, fps, durationMs);

    struct colour currentIncrement = increment;
    for( int i = 0; i < fps; i++ )
    {
        transitionStep( begin, final , currentIncrement, diode);
        sleep_ms(  durationMs / fps );
        currentIncrement.red += increment.red;
        currentIncrement.blue += increment.blue;
        currentIncrement.green += increment.green; 
    }
}

int main( ) 
{
    stdio_init_all( );
    
    struct colour red = { 255, 0, 0 };
    struct colour blue = { 0, 0, 255 };
    struct colour green = { 0, 255, 0 };
    struct colour white = { 255, 255, 255 };
    struct colour black = { 0, 0, 0 }; 
    struct colour yelow = {255, 255, 0,};
    struct colour gold = { 255, 215, 0 };
    struct colour orange = { 255, 165, 0 };
    struct colour orangeRed = { 255, 69, 0 };

    
    struct ledRGB diode = { 16, 28, 17 };
    
    initRGB( diode );

while( 1 )
{
    
    while (1)
    {
        colourTransition( yelow, red, 30, 4000, diode );
        
        colourTransition( red, yelow, 30, 7000, diode );
        

    }
    
}   

}
