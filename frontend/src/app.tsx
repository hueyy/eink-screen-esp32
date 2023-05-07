import { Route, Router } from 'preact-router'
import HomePage from './pages/home'
import TextPage from './pages/text'

export const App = () => {

  return (
    <Router>
      <Route default path="/" component={HomePage} />
      <Route path="/text" component={TextPage} />
    </Router>
  )
}
