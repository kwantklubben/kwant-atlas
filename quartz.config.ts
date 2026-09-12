import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Kwant Atlas",
    pageTitleSuffix: " | KwantKlubben",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "plausible",
    },
    locale: "en-US",
    baseUrl: "atlas.kwantklubben.com",
    ignorePatterns: ["private", "templates", ".obsidian", "**/_legacy/**"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Space Grotesk",
        body: "Space Grotesk",
        code: "Space Mono",
      },
      colors: {
        lightMode: {
          light: "#0C1016",
          lightgray: "#1E2530",
          gray: "#5A6677",
          darkgray: "#DCD4BD",
          dark: "#FBF9F2",
          secondary: "#C2EB2B",
          tertiary: "#D5F25A",
          highlight: "rgba(194, 235, 43, 0.15)",
          textHighlight: "#C2EB2B88",
        },
        darkMode: {
          light: "#0C1016",
          lightgray: "#1E2530",
          gray: "#5A6677",
          darkgray: "#DCD4BD",
          dark: "#FBF9F2",
          secondary: "#C2EB2B",
          tertiary: "#D5F25A",
          highlight: "rgba(194, 235, 43, 0.15)",
          textHighlight: "#C2EB2B88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: true }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // CustomOgImages disabled to prevent sharp build dependencies
      // Plugin.CustomOgImages(),
    ],
  },
}

export default config
