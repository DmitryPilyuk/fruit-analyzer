using static FruitComponent.FruitChart;

namespace FruitAnalyzerFront.Blazor.Scripts
{
    public static class FruitChartExtension
    {
        public static string[] ToColorArray(this FruitChartItem[] fruitChartItems)
        {
            if (fruitChartItems == null)
                return Array.Empty<string>();

            var resultColors = new List<string>();

            foreach (var item in fruitChartItems)
            {
                switch (item.Fruit.ToLower())
                {
                    case "banana":
                        resultColors.Add("#fffbc9");
                        break;
                    case "apple":
                        resultColors.Add("#8b0202");
                        break;
                    case "grapes":
                        resultColors.Add("#abe16b");
                        break;
                    case "orange":
                        resultColors.Add("#ffa500");
                        break;
                    case "pineapple":
                        resultColors.Add("#ffbd35");
                        break;
                    default:
                        throw new Exception("Can't recognize fruit color!");
                }
            }

            return resultColors.ToArray();
        }

        public static FruitChartItem FindFruitWithMaxProbability(this FruitChartItem[] chartItems)
        {
            if (chartItems == null || chartItems.Length == 0)
                throw new Exception("Can't find fruit in empty list!");

            // Find max by comparing all fruits
            var maxChartItem = chartItems.Aggregate((max, current) => current.Probability > max.Probability ? current : max);

            return maxChartItem;
        }
    }
}
