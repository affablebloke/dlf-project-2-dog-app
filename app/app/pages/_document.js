import Document, { Head, Main, NextScript } from 'next/document'
import flush from 'styled-jsx/server'

export default class MyDocument extends Document {
  static getInitialProps({ renderPage }) {
    const { html, head, errorHtml, chunks } = renderPage()
    const styles = flush()
    return { html, head, errorHtml, chunks, styles }
  }

  render() {
    return (
      <html>
        <Head>
          <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" />
        </Head>
        <body>
          {this.props.customValue}
          <Main />
          <NextScript />
        </body>
        <style global jsx>{`
        body{
          background: #40555f;
          min-width: 900px;
        }
        * {
            font-smoothing: antialiased;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Roboto;
            text-decoration: none;
        }
    `}</style>
      </html>
    )
  }
}