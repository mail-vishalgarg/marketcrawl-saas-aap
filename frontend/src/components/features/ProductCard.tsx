import type { ProductCard as ProductCardType } from '../../types';
import styles from './ProductCard.module.css';

export function ProductCard({ asin, title, price, rating, image_url }: ProductCardType) {
  return (
    <a
      className={styles.card}
      href={`https://www.amazon.com/dp/${asin}`}
      target="_blank"
      rel="noreferrer"
    >
      <div className={styles.imageWrap}>
        {image_url
          ? <img src={image_url} alt={title} className={styles.image} />
          : <div className={styles.noImage}>No image</div>
        }
      </div>
      <div className={styles.info}>
        <div className={styles.title}>{title}</div>
        <div className={styles.meta}>
          {price && <span className={styles.price}>{price}</span>}
          {rating != null && rating > 0 && <span className={styles.rating}>★ {rating}</span>}
        </div>
      </div>
    </a>
  );
}
