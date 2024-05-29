import React, { useState } from 'react';
import ArticleViewer from './ArticleViewer';
import ArticleList from './ArticleList';

const App = () => {
  const [selectedArticleId, setSelectedArticleId] = useState(null);

  const handleSelectArticle = (id) => {
    setSelectedArticleId(id);
  };

  const handleBackToList = () => {
    setSelectedArticleId(null);
  };

  return (
    <div>
      {selectedArticleId ? (
        <ArticleViewer
          articleId={selectedArticleId}
          onBackToList={handleBackToList}
        />
      ) : (
        <ArticleList onSelectArticle={handleSelectArticle} />
      )}
    </div>
  );
};

export default App;
