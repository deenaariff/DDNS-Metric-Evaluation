package routing;

import ledger.Ledger;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.NoSuchElementException;

public class RoutingTable {

	private List<Route> table;
	private HashMap<Integer,Route> id_map;

	// Data Structures used by Leader
    private HashMap<Route,Integer> matchIndex;
    private HashMap<Route,Integer> nextIndex;

    // Watchers listening for leader election changes
    private List<Route> watchers;

    /**
     * Constructor for Routing Table
     * @param configFile
     * @param ledger
     */
	public RoutingTable(String configFile, Ledger ledger) {
	    this.id_map = new HashMap<Integer, Route>();
        this.table = new ArrayList<Route>();
        this.matchIndex = new HashMap<Route, Integer>();
        this.nextIndex = new HashMap<Route,Integer>();
        this.watchers = new ArrayList();
        this.configToTable(configFile); // this will initialize next, index in the routing table for us
    }

    /**
     * Get the next Index for a particular Route
     * @param route
     * @return
     */
	public int getNextIndex(Route route) {
	    try {
            return nextIndex.get(route);
        } catch (NoSuchElementException e) {
	        e.printStackTrace();
	        System.exit(1);
        }
        return -1;
    }

    /**
     * Get the next Index for a particular Route
     * @param route
     * @return
     */
    public int getMatchIndex(Route route) {
        try {
            return matchIndex.get(route);
        } catch (NoSuchElementException e) {
            e.printStackTrace();
            System.exit(1);
        }
        return -1;
    }

    /**
     * Update the matchIndex and nextIndex simulataneously
     * by a given amount
     */
    public void updateServerIndex(Route route, int increment) {
        int new_mi = Math.max(0,this.matchIndex.get(route) + increment);
        int new_ni = Math.max(0,this.nextIndex.get(route) + increment);
        this.matchIndex.put(route,new_mi);
        this.nextIndex.put(route,new_ni);
    }

    /**
     * Add a new entry to the RoutingTable
     * @param ip
     * @param heartbeat_port
     * @param voting_port
     */
	public void addEntry(String ip, int heartbeat_port, int voting_port) {
		this.table.add(new Route(ip, heartbeat_port, voting_port));
	}

    /**
     * Get the Routing information for a given id
     * @param id
     * @return
     */
    public Route getRouteById(Integer id) {
        try {
            return id_map.get(id);
        } catch (Exception e) {
            throw new RuntimeException("Route not available for this id");
        }
    }

    /**
     * Construct the Routing Table Given the Appropriate xml file
     *
     * @param configFile
     * @return
     */
    private void configToTable(String configFile) {

        try {
            InputStream is = new FileInputStream(new File(configFile)); // Grab from absolute path of config file
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(is);

            doc.getDocumentElement().normalize();
            NodeList nList = doc.getElementsByTagName("node");

            for (int temp = 0; temp < nList.getLength(); temp++) {
                Node nNode = nList.item(temp);
                Route new_route = new Route();

                if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) nNode;
                    Integer id = initializeRouteFromElement(eElement, new_route);  // Initialize new_route info and assign the route to its id
                    this.id_map.put(id,new_route);
                }

                this.matchIndex.put(new_route,0); // initialize match index to 0
                this.nextIndex.put(new_route,0); // initialize nextIndex to 0

                this.table.add(new_route); // Add to the routing table
            }

            NodeList wList = doc.getElementsByTagName("watcher");

            for (int i = 0; i < wList.getLength(); i++) {
                Node wNode = wList.item(i);
                Route watcher = new Route();

                if(wNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element eElement = (Element) wNode;
                    initializeWatcherFromElement(eElement,watcher);
                }

                this.watchers.add(watcher);
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    /**
     * Set fields for a route given an Element Object
     * @param eElement
     * @param new_route
     * @return
     */
    private static int initializeRouteFromElement(Element eElement, Route new_route) {
        Integer id = Integer.parseInt(eElement.getAttribute("id"));
        new_route.setId(id);
        new_route.setIP(eElement.getElementsByTagName("ip").item(0).getTextContent());
        new_route.setEndpointPort(Integer.parseInt(eElement.getElementsByTagName("client").item(0).getTextContent()));
        new_route.setHeartBeatPort(Integer.parseInt(eElement.getElementsByTagName("heartbeat").item(0).getTextContent()));
        new_route.setVotingPort(Integer.parseInt(eElement.getElementsByTagName("voting").item(0).getTextContent()));
        return id;
    }

    /**
     * Set fields for a Watcher route given an Element Object
     * @param eElement
     * @param watcher
     */
    private static void initializeWatcherFromElement(Element eElement, Route watcher) {
        watcher.setIP(eElement.getElementsByTagName("ip").item(0).getTextContent());
        watcher.setEndpointPort(Integer.parseInt(eElement.getElementsByTagName("port").item(0).getTextContent()));
    }

    /**
     * This method returns the number of nodes it would take to specify the
     * majority of the cluster.
     * @return
     */
    public Integer getMajority() {
        return (int) Math.ceil(this.table.size() / 2);
    }

    /** Standard Getters and Setters */
    public List<Route> getTable() { return this.table; }

    public List<Route> getWatchers () { return this.watchers; }

    public boolean hasWatchers () { return this.watchers.size() > 0; }



}



