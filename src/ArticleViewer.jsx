import React, { useState, useEffect } from 'react';

const ArticleViewer = () => {
  const [article, setArticle] = useState(null);
  const [articleId, setArticleId] = useState(1); // starting with article ID 1
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchArticle(articleId);
  }, [articleId]);

  const fetchArticle = async (id) => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${id}`
      );
      const data = await response.json();
      // Add some mock photos to the data
      data.photos = [
        `https://picsum.photos/seed/${id}/200/150`,
        `https://picsum.photos/seed/${id + 1}/200/150`,
      ];
      setArticle(data);
    } catch (error) {
      console.error('Error fetching article:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const orderArticle = () => {
    // Implement order article functionality
    console.log('Order article:', article.id);
    // Add API call or order logic here
  };

  const addToFavorites = () => {
    // Implement add to favorites functionality
    console.log('Add to favorites:', article.id);
    // Add API call or favorite logic here
  };

  const nextArticle = () => {
    setArticleId((prevId) => prevId + 1);
  };

  const prevArticle = () => {
    setArticleId((prevId) => (prevId > 1 ? prevId - 1 : 1));
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!article) {
    return <div>No article found</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.navButton} onClick={prevArticle}>
          prev
        </button>
        <div style={styles.articleName}>{article.title}</div>
        <button style={styles.navButton} onClick={nextArticle}>
          next
        </button>
      </div>
      <div style={styles.photoStrip}>
        {article.photos &&
          article.photos.map((photo, index) => (
            <img
              key={index}
              src={photo}
              alt={`Article ${index}`}
              style={styles.photo}
            />
          ))}
      </div>
      <div style={styles.articleDescription}>{article.body}</div>
      <div style={styles.footer}>
        <button
          style={styles.footerButton}
          onClick={() => console.log('Go to list')}
        >
          to list
        </button>
        <button style={styles.orderButton} onClick={orderArticle}>
          order article
        </button>
        <button style={styles.footerButton} onClick={addToFavorites}>
          ⭐
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    border: '2px solid black',
    width: '300px',
    margin: '0 auto',
    padding: '10px',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '2px solid black',
    paddingBottom: '10px',
    marginBottom: '10px',
  },
  navButton: {
    padding: '10px',
  },
  articleName: {
    flex: 1,
    textAlign: 'center',
  },
  photoStrip: {
    border: '2px solid black',
    padding: '10px',
    textAlign: 'center',
    marginBottom: '10px',
  },
  photo: {
    maxWidth: '100%',
    maxHeight: '100px',
    margin: '5px',
  },
  articleDescription: {
    flex: 1,
    border: '2px solid black',
    padding: '10px',
    marginBottom: '10px',
    textAlign: 'center',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTop: '2px solid black',
    paddingTop: '10px',
    marginTop: '10px',
  },
  footerButton: {
    padding: '10px',
  },
  orderButton: {
    flex: 1,
    padding: '10px',
    textAlign: 'center',
    margin: '0 10px',
  },
};

export default ArticleViewer;
