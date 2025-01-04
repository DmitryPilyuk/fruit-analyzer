using System.Text.Json;

namespace FruitAnalyzerFront.AppLogic
{
    public class UploadedFileData
    {
        public int FileSize { get; set; }
        public required string FileName { get; set; }
        public required string ContentType { get; set; }
    }
    public class FruitProbabilityData
    {
        public double Banana { get; set; }
        public double Apple { get; set; }
        public double Grapes { get; set; }
        public double Orange { get; set; }
        public double Pineapple { get; set; }
    }

    public class ErrorResponseData
    {
        public required string ErrorMessage { get; set; }
    }

    public class APIException : Exception
    {
        public APIException(string message) : base(message) { }
    }

    public static class FruitAPI
    {
        private const string URI = "http://127.0.0.1:8000";

        private const string URI_UPLOAD_IMAGE = $"{URI}/uploadimage/";
        private const string URI_ANALYZE_IMAGE = $"{URI}/analyzeimage/";

        private const string FORM_DATA_IMAGE_KEY = "image";

        public static async Task UploadImage(byte[] imageBytes, string imageName)
        {
            using (var client = new HttpClient())
            {
                using (var content = new MultipartFormDataContent())
                {
                    content.Add(new StreamContent(new MemoryStream(imageBytes)), FORM_DATA_IMAGE_KEY, imageName);

                    using (
                       var message =
                           await client.PostAsync(URI_UPLOAD_IMAGE, content))
                    {

                        var responseJson = await ReadAPIResponseAsync<UploadedFileData>(message);

                        if (responseJson.FileSize == imageBytes.Length && responseJson.FileName == imageName)
                            return;
                        else
                            throw new APIException("Receive incorrect image data");
                    }
                }
            }
        }

        public static async Task<FruitProbabilityData> AnalyzeFruit(string imageName)
        {
            using (var client = new HttpClient())
            {
                using (var content = new MultipartFormDataContent())
                {
                    using (
                       var message = await client.GetAsync(GetAnalyzeUri(imageName)))
                    {

                        var responseJson = await ReadAPIResponseAsync<FruitProbabilityData>(message);

                        return responseJson;
                    }
                }
            }
        }

        private static string GetAnalyzeUri(string filename) => URI_ANALYZE_IMAGE + filename;

        private static async Task<T> ReadAPIResponseAsync<T>(HttpResponseMessage message)
        {
            message.EnsureSuccessStatusCode();
            var responseStream = await message.Content.ReadAsStreamAsync();

            try
            {
                var responseJson = await JsonSerializer.DeserializeAsync<T>(responseStream);

                if (responseJson != null)
                    return responseJson;
                else
                    throw new Exception();
            }
            catch (Exception)
            {
                responseStream.Seek(0, SeekOrigin.Begin);
                var responseErrorJson = await JsonSerializer.DeserializeAsync<ErrorResponseData>(responseStream);

                throw new APIException(responseErrorJson?.ErrorMessage ?? "Can't get error message from response :(");
            }
        }

    }
}
