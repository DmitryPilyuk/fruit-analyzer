using System.Text.Json;

namespace FruitAnalyzerFront.AppLogic
{
    public class UploadedFileData
    {
        /// <summary>
        /// Decoded API-response file data
        /// </summary>
        public int file_size { get; set; }
        public required string file_name { get; set; }
        public required string content_type { get; set; }
    }
    public class FruitProbabilityData
    {
        /// <summary>
        /// Decoded API-response probability data
        /// </summary>
        public double apple { get; set; }   
        public double banana { get; set; }
        public double grape { get; set; }
        public double kiwi { get; set; }
        public double orange { get; set; }
        public double pineapple { get; set; }
        public double pomegranate { get; set; }
        public double watermelon { get; set; }

    }

    public static class AnalyzeModelName
    {
        public const string BasicModel = "basic_model";
        public const string ColorModel = "color_model";
        public const string LeafModel = "leaf_model";
        public const string ShapeModel = "shape_model";
        public const string StructureModel = "structure_model";
        public const string TextureModel = "texture_model";
    }

    public class ErrorResponseData
    {
        /// <summary>
        /// Decoded error API-response
        /// </summary>
        public required string error_message { get; set; }
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

                        if (responseJson.file_size == imageBytes.Length && responseJson.file_name == imageName)
                            return;
                        else
                            throw new APIException("Receive incorrect image data");
                    }
                }
            }
        }

        public static async Task<FruitProbabilityData> AnalyzeFruit(string imageName, string modelName)
        {
            using (var client = new HttpClient())
            {
                using (var content = new MultipartFormDataContent())
                {
                    using (
                       var message = await client.GetAsync(GetAnalyzeUri(imageName, modelName)))
                    {

                        var responseJson = await ReadAPIResponseAsync<FruitProbabilityData>(message);

                        return responseJson;
                    }
                }
            }
        }

        private static string GetAnalyzeUri(string filename, string model_name = AnalyzeModelName.BasicModel) => 
            URI_ANALYZE_IMAGE + filename + '\\' + model_name;

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

                throw new APIException(responseErrorJson?.error_message ?? "Can't get error message from response :(");
            }
        }

    }
}
