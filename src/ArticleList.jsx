import React, { useState, useEffect } from 'react';

const ArticleList = ({ onSelectArticle }) => {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchArticles();
  }, []);

  const fetchArticles = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        'https://jsonplaceholder.typicode.com/posts'
      );
      const data = await response.json();
      setArticles(data);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={listStyles.container}>
      {articles.map((article) => (
        <div
          key={article.id}
          style={listStyles.articleItem}
          onClick={() => onSelectArticle(article.id)}
        >
          {article.title}
        </div>
      ))}
    </div>
  );
};

const listStyles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    border: '2px solid black',
    width: '300px',
    margin: '0 auto',
    padding: '10px',
  },
  articleItem: {
    padding: '10px',
    borderBottom: '1px solid black',
    cursor: 'pointer',
  },
};

export default ArticleList;
