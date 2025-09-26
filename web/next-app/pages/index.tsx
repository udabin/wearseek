import { useState } from "react";

export default function Home(){
  const [q,setQ]=useState("");
  const [items,setItems]=useState<any[]>([]);
  const onSearch=async()=>{
    const r = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    const j = await r.json(); setItems(j.items||[]);
  };
  return (
    <main style={{maxWidth:920, margin:"40px auto", fontFamily:"system-ui"}}>
      <h1>WearSeek</h1>
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="예: 검정 오버핏 반팔" style={{width:"70%"}}/>
      <button onClick={onSearch}>검색</button>
      <ul>
        {items.map((x)=>(
          <li key={x._id} style={{display:"flex", gap:12, padding:"10px 0", borderBottom:"1px solid #eee"}}>
            <img src={x.image_url} width={80}/>
            <div>
              <a href={x.url} target="_blank"><b>{x.title}</b></a>
              <div>{x.brand} · {x.price?.toLocaleString()} {x.currency} · {x.color_std}</div>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}