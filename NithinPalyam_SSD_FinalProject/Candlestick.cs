using System;
using System.Collections.Generic;

namespace NithinPalyam_SSD_FinalProject
{
    internal class Candlestick
    {
       
        public Candlestick()
        {


        }
    }

    public class CandlestickData
    {
        public string Ticker { get; set; }
        public string Period { get; set; }
        public DateTime Date { get; set; }
        public decimal Open { get; set; }
        public decimal High { get; set; }
        public decimal Low { get; set; }
        public decimal Close { get; set; }
        public int Volume { get; set; }
    }
}