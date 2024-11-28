using System.Text.RegularExpressions;

namespace Whatsthis.API.Utilities
{
    public static partial class UrlHelper
    {
        [GeneratedRegex(@"^(?!https?://)(\S+)$")]
        private static partial Regex UrlRegexAddHttps();

        [GeneratedRegex(@"^(https?:\/\/)?([^\/]+)(\/.*)?$")]
        private static partial Regex ExtractDomain();

        public static string CleanUrl(string url)
        {
            return ExtractDomain().Replace(url, "$2");
        }

        public static string CleanUrlAlternative(string url)
        {
            return UrlRegexAddHttps().Replace(url, "https://$1");
        }
    }
}
