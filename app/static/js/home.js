var landingPart = React.createClass({
  render: function() {
    return (
      <div>
        <a name="about" />
        <div className="intro-header">
          <div className="container">
            <div className="row">
              <div className="col-lg-12">
                <div className="intro-message">
                  <h1>クックパッド採用課題</h1>
                  <h3>写真掲示アプリケーションMugistagram</h3>
                  <hr className="intro-divider" />
                  <ul className="list-inline intro-social-buttons">
                    <li>
                      <a href="/login" className="btn btn-success btn-lg">新規登録</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
});

React.render(
	React.createElement(landingPart, null),
	document.getElementById('about')
);

