using FruitAnalyzerFront.Components;
using Radzen;

namespace FruitAnalyzerFront
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
            builder.Services.AddRazorComponents()
                .AddInteractiveServerComponents();

            // Now app Radzen Components can be used in App 
            builder.Services.AddRadzenComponents();

            var webApp = builder.Build();

            webApp.UseStaticFiles();
            webApp.UseAntiforgery();

            webApp.MapRazorComponents<App>()
                .AddInteractiveServerRenderMode();

            webApp.Run();
        }
    }
}
