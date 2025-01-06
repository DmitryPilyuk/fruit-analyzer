using FruitAnalyzerFront.AppLogic;
using static FruitComponent.FruitChart;

namespace FruitAnalyzerFront.Blazor.Scripts
{
    public static class APIExtension
    {
        public static FruitChartItem[] ToFruitChartItems(this FruitProbabilityData apiData)
        {
            if (apiData == null)
                return Array.Empty<FruitChartItem>();

            var resultChartItems = new List<FruitChartItem>();

            resultChartItems.Add(new FruitChartItem { Fruit = "Banana", Probability = Math.Round(apiData.Banana, 2) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Apple", Probability = Math.Round(apiData.Apple, 2) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Grapes", Probability = Math.Round(apiData.Grapes, 2) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Orange", Probability = Math.Round(apiData.Orange, 2) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Pineapple", Probability = Math.Round(apiData.Pineapple, 2) });

            return resultChartItems.ToArray();
        }
    }
}
