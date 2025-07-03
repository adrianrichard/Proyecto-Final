"Example of passing in data and creating standalone charts"

from rml.vbarchart import ThermometerChart
from gen_report import compute_bar_heights



def run():
    state_average_emissions = 10.7
    customer_emissions = 12.1
    p1 = 42
    p2 = 23
    p3 = 17
    create_bitmap(state_average_emissions, customer_emissions, p1, p2, p3, prefix='thermometer-test-1')


    state_average_emissions = 14.7
    customer_emissions = 12.1
    p1 = 42
    p2 = 23
    p3 = 17
    create_bitmap(state_average_emissions, customer_emissions, p1, p2, p3, prefix='thermometer-test-2')

    state_average_emissions = 14.7
    customer_emissions = 12.1
    p1 = 0
    p2 = 29
    p3 = 23
    create_bitmap(state_average_emissions, customer_emissions, p1, p2, p3, prefix='thermometer-test-3')

    state_average_emissions = 14.7
    customer_emissions = 12.1
    p1 = 51
    p2 = 0
    p3 = 29
    create_bitmap(state_average_emissions, customer_emissions, p1, p2, p3, prefix='thermometer-test-4')



def create_bitmap(state_average_emissions, customer_emissions, p1, p2, p3, prefix='test'):
    """Instantiate a chart and set the bits which vary depending on data


    This code largely duplicates what's in gen_report.py for PDF creation
    """

    c = ThermometerChart()

    heights = compute_bar_heights(state_average_emissions, customer_emissions, p1, p2, p3)
    prev = 0
    thermometer_chart_data = []
    for h in heights:
        delta = h - prev
        thermometer_chart_data.append([delta])
        prev = h



    if state_average_emissions > customer_emissions:
        label4 = "Your starting point"
        label5 = "State average"
    else:
        label5 = "Your starting point"
        label4 = "State average"

   
    c._chart_data = thermometer_chart_data


    # upper two labels may switch around depending on value
    c._l4text = label4
    c._l5text = label5


    c.save(formats=['pdf', 'svg'],outDir='.',fnRoot=prefix)


    # now we want it sharp.  Default of 72dpi is grainy.  Make the bitmap 4 times bigger,
    # and make the chart on the drawing 4x bigger too
    c.renderScale = 4.0
    c.save(formats=['png'],outDir='.',fnRoot=prefix, _renderPM_dpi=4 * 72)



    # c.chart.data =  compute_bar_heights(14.7, 12.1, 32, 33, 17)
    # c.save(formats=['pdf','png'],outDir='.',fnRoot="thermometer-test-2")




if __name__=='__main__':
    run()
