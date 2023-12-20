using System;

public class Candelstick
{
	public Candelstick()
	{
        private List<candlestick> templist = new List<candlestick>
        string filePath = $".csv";
        using (var reader = new StreamReader(filePath))
        using (var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture)))
        {
            return csv.GetRecords<StockData>().ToList();
        }

        List<StockData> stockData = LoadStockData(selectedTicker, "Day");
        dataGridView1.DataSource = stockData;

    }
    
    public CandlestickChart(Chart chart)
    {
        this.chart = chart;
        InitializeChart();
    }


}
