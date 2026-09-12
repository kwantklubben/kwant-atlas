import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "KwantKlubben": "https://kwantklubben.com",
      "GitHub Organization": "https://github.com/kwantklubben",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
                { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer({
      // hide the site home from the tree (it isn't one of the top-level items)
      filterFn: (node) => node.slugSegment !== "tags" && node.slugSegment !== "index",
      // flatten the "pillars" wrapper so Pillar 1-8 sit at the tree's top level
      mapFn: (node) => {
        const idx = node.children?.findIndex((c) => c.slugSegment === "pillars" && c.isFolder) ?? -1
        if (idx >= 0) {
          const pillars = node.children[idx]
          node.children.splice(idx, 1, ...pillars.children)
        }
        return node
      },
    }),
  ],
  right: [
    Component.DesktopOnly(Component.Graph()),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
              ],
    }),
    Component.Explorer({
      // hide the site home from the tree (it isn't one of the top-level items)
      filterFn: (node) => node.slugSegment !== "tags" && node.slugSegment !== "index",
      // flatten the "pillars" wrapper so Pillar 1-8 sit at the tree's top level
      mapFn: (node) => {
        const idx = node.children?.findIndex((c) => c.slugSegment === "pillars" && c.isFolder) ?? -1
        if (idx >= 0) {
          const pillars = node.children[idx]
          node.children.splice(idx, 1, ...pillars.children)
        }
        return node
      },
    }),
  ],
  right: [],
}
