using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using static Project3.Candlestick;
using static Project3.EnterData_Form;
using static Project3.SmartCandlestick;
using static Project3.PatternRecognizer;

namespace Project3
{
    public partial class Display_Form : Form
    {
        List<CandlestickData> DisplaycandlestickDataList = new List<CandlestickData>();
        public List<EnterData_Form> CreatedFormsList { get; set; }
        List<PatternRecognizer> patternRecognizers;
        internal Candlestick candlestick = new Candlestick();
        //SmartCandlestick smartcandlestick = new SmartCandlestick();

        public Display_Form()
        {
            InitializeComponent();
            // Set the current directory to the base directory of the application
            Directory.SetCurrentDirectory(AppDomain.CurrentDomain.BaseDirectory);

            // Initialize the Candlestick object
            candlestick = new Candlestick();

            InitializeComboBox();

            // Set X and Y value members for the series (adjust these based on your data structure)
            chart1.Series["CandlestickSeries"].XValueMember = "Date";
            chart1.Series["CandlestickSeries"].YValueMembers = "Open,High,Low,Close";

            chart1.Series["VolumnSeries"].XValueMember = "Date";
            chart1.Series["VolumnSeries"].YValueMembers = "Volume";
        }


        private void button2_Click_1(object sender, EventArgs e)
        {
            string selectedPattern = comboBox1.SelectedItem?.ToString();
            DateTime startDate = dateTimePicker1.Value;
            DateTime endDate = dateTimePicker2.Value;

            SmartCandlestick smartCandlestick = new SmartCandlestick();
            PatternRecognizer selectedRecognizer = smartCandlestick.FindPatternRecognizerByName(selectedPattern);


            foreach (Form openForm in Application.OpenForms)
            {
                if (openForm is Display_Form form && form.Tag != null)  
                {
                    string filePath = form.Tag.ToString();
                    List<CandlestickData> candlestickDataList = candlestick.LoadData(filePath, startDate, endDate, selectedPattern);
                    UpdateFormInputParameters(form, startDate, endDate, selectedPattern, candlestickDataList);
                }
            }
        }

        public List<CandlestickData> IsDateInRange(List<CandlestickData> candlestickDataList, DateTime startDate, DateTime endDate)
        {
            List<CandlestickData> filteredCandlestickList = new List<CandlestickData>();

            foreach (CandlestickData data in candlestickDataList)
            {
                if (data.Date >= startDate && data.Date <= endDate)
                {
                    filteredCandlestickList.Add(data);
                }
            }

            return filteredCandlestickList;
        }

        public void UpdateCandlestickChart(List<CandlestickData> candlestickDataList)
        {
            try
            {
                chart1.DataSource = candlestickDataList;
                chart1.DataBind();
                Annotate_thechart(chart1, PatternRecognizer.RecognizePatterns(candlestickDataList));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error updating chart: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            return;

        }


        public void UpdateFormInputParameters(Display_Form form, DateTime startDate, DateTime endDate, string patternType, List<CandlestickData> candlestickDataList)
        {
            // Update the input parameters for the specified form
            List<CandlestickData> filteredCandlestickList = IsDateInRange(candlestickDataList, startDate, endDate);
            UpdateCandlestickChart(filteredCandlestickList);
            // MessageBox.Show($"Start Date: {startDate}, End Date: {endDate}, Pattern Type: {patternType}");
        }

        private void AddRectangularAnnotation(Chart chart, DateTime date, decimal high, decimal low)
        {
            // Add a rectangular annotation around the candlestick
            var annotation = new RectangleAnnotation
            {
                AxisX = chart.ChartAreas[0].AxisX,
                AxisY = chart.ChartAreas[0].AxisY,
                X = date.ToOADate(),
                Y = Convert.ToDouble(high),
                Width = 1,  // Adjust the width as needed
                Height = Convert.ToDouble(high - low),
                BackColor = Color.Transparent,  // Set the background color as needed
                LineColor = Color.Red,  // Set the border color as needed
                LineWidth = 2,  // Set the border width as needed
                LineDashStyle = ChartDashStyle.Solid  // Set the border dash style as needed
            };

            chart.Annotations.Add(annotation);
        }

        public void Annotate_thechart(Chart chart, List<PatternRecognizer> patternRecognizers)
        {
            foreach (PatternRecognizer recognizer in patternRecognizers)
            {
                // Recognize patterns and get the list of indices
                List<int> recognizedIndices = recognizer.RecognizePatterns(DisplaycandlestickDataList);

                foreach (int index in recognizedIndices)
                {
                    // Access the corresponding CandlestickData from the DisplaycandlestickDataList
                    if (index >= 0 && index < DisplaycandlestickDataList.Count)
                    {
                        CandlestickData candlestickData = DisplaycandlestickDataList[index];

                        // Annotate the chart based on the recognized indices
                        AddRectangularAnnotation(chart, candlestickData.Date, candlestickData.High, candlestickData.Low);
                    }
                }
            }
        }

        private void InitializeComboBox()
        {
            foreach (PatternRecognizer recognizer in PatternRecognizerList)
            {
                comboBox1.Items.Add(recognizer.PatternName);
            }
        }

        private void chart1_Click_1(object sender, EventArgs e)
        {

        }

        private void display_Form_Load(object sender, EventArgs e)
        {

        }
    }
}
