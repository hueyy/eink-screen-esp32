import { Route, Router } from 'preact-router'
import HomePage from './pages/home'
import TextPage from './pages/text'
import ImagePage from './pages/image'
import type { FunctionComponent } from 'preact'

export const App: FunctionComponent = () => {
  return (
    <Router>
      <Route default path="/" component={HomePage} />
      <Route path="/text" component={TextPage} />
      <Route path="/image" component={ImagePage} />
    </Router>
  )
}
