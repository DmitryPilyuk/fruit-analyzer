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

            resultChartItems.Add(new FruitChartItem { Fruit = "Banana", Probability = CalculateProbability(apiData.banana)});
            resultChartItems.Add(new FruitChartItem { Fruit = "Apple", Probability = CalculateProbability(apiData.apple) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Grapes", Probability = CalculateProbability(apiData.grape) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Orange", Probability = CalculateProbability(apiData.orange) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Pineapple", Probability = CalculateProbability(apiData.pineapple) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Watermelon", Probability = CalculateProbability(apiData.watermelon) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Pomegranate", Probability = CalculateProbability(apiData.pomegranate) });
            resultChartItems.Add(new FruitChartItem { Fruit = "Kiwi", Probability = CalculateProbability(apiData.kiwi) });

            return resultChartItems.ToArray();
        }

        private static double CalculateProbability(double prob) => Math.Round(prob * 100, 2);
    }
}
